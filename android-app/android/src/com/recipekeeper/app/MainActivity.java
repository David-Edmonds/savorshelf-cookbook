package com.recipekeeper.app;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.util.AtomicFile;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.Toast;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/** Bundled app shell. Optional native HTTPS generation; remote executable content is never loaded. */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final int PICK_FILE = 42, SAVE_FILE = 43;
    private WebView web;
    private FrameLayout root;
    private AtomicFile store;
    private ValueCallback<Uri[]> fileCallback;
    private String pendingExport;
    private final java.util.concurrent.atomic.AtomicReference<String> sharedRecipe = new java.util.concurrent.atomic.AtomicReference<>("");
    private final java.util.concurrent.atomic.AtomicBoolean aiBusy = new java.util.concurrent.atomic.AtomicBoolean(false);
    private volatile boolean destroyed=false;

    @Override public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        configureEdgeToEdge();
        if (android.os.Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(
                android.window.OnBackInvokedDispatcher.PRIORITY_DEFAULT, () -> handleBack());
        }
        store = new AtomicFile(new File(getFilesDir(), "recipes-v1.json"));
        root = new FrameLayout(this);
        root.setBackgroundColor(Color.rgb(247,241,232));
        setContentView(root);
        root.setOnApplyWindowInsetsListener((v, insets) -> {
            if (android.os.Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets i = insets.getInsets(WindowInsets.Type.systemBars()
                    | WindowInsets.Type.displayCutout() | WindowInsets.Type.ime());
                v.setPadding(i.left,i.top,i.right,i.bottom);
                return WindowInsets.CONSUMED;
            }
            int left=insets.getSystemWindowInsetLeft(), top=insets.getSystemWindowInsetTop();
            int right=insets.getSystemWindowInsetRight(), bottom=insets.getSystemWindowInsetBottom();
            if (android.os.Build.VERSION.SDK_INT >= 28 && insets.getDisplayCutout()!=null) {
                android.view.DisplayCutout cutout=insets.getDisplayCutout();
                left=Math.max(left,cutout.getSafeInsetLeft());top=Math.max(top,cutout.getSafeInsetTop());
                right=Math.max(right,cutout.getSafeInsetRight());bottom=Math.max(bottom,cutout.getSafeInsetBottom());
            }
            v.setPadding(left,top,right,bottom);
            return insets.consumeSystemWindowInsets();
        });
        root.requestApplyInsets();
        try { web = new WebView(this); }
        catch (RuntimeException error) { showWebViewHelp(); return; }
        String agent=web.getSettings().getUserAgentString();
        java.util.regex.Matcher chrome=java.util.regex.Pattern.compile("Chrome/(\\d+)").matcher(agent);
        if(!chrome.find() || Integer.parseInt(chrome.group(1))<80) { web.destroy(); web=null; showWebViewHelp(); return; }
        web.setBackgroundColor(Color.rgb(247,241,232));
        root.addView(web, new FrameLayout.LayoutParams(-1,-1));
        applyAppearance(isSystemDarkMode());
        web.getSettings().setJavaScriptEnabled(true);
        web.getSettings().setDomStorageEnabled(true);
        web.getSettings().setAllowFileAccess(false);
        web.getSettings().setAllowContentAccess(true); // Only explicitly selected SAF document URIs.
        web.getSettings().setBlockNetworkLoads(true);
        web.getSettings().setMixedContentMode(android.webkit.WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        web.getSettings().setSupportMultipleWindows(false);
        WebView.setWebContentsDebuggingEnabled(false);
        web.addJavascriptInterface(new LocalBridge(), "AndroidBridge");
        web.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                if (isLocal(r.getUrl())) return false;
                Uri target=r.getUrl();
                if (r.isForMainFrame() && r.hasGesture() &&
                    ("https".equals(target.getScheme()) || "mailto".equals(target.getScheme()))) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW,target)); }
                    catch (Exception error) { message("No app could open that support link."); }
                }
                return true;
            }
            @Override public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest r) {
                Uri uri=r.getUrl();
                if(!isLocal(uri)||!"GET".equals(r.getMethod())) return denied();
                String path=uri.getPath();
                if(path==null||!path.startsWith("/assets/")||path.contains("..")||path.contains("\\")) return denied();
                path=path.substring(8);
                if(path.isEmpty()) path="index.html";
                try {
                    InputStream input=getAssets().open(path);
                    String mime=path.endsWith(".js")?"application/javascript":path.endsWith(".css")?"text/css":path.endsWith(".svg")?"image/svg+xml":path.endsWith(".png")?"image/png":path.endsWith(".jpg")||path.endsWith(".jpeg")?"image/jpeg":path.endsWith(".webp")?"image/webp":path.endsWith(".json")||path.endsWith(".webmanifest")?"application/json":"text/html";
                    Map<String,String> headers=new HashMap<>();
                    headers.put("Content-Security-Policy", "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; manifest-src 'self'; base-uri 'none'; form-action 'none'");
                    headers.put("X-Content-Type-Options","nosniff");
                    return new WebResourceResponse(mime,"UTF-8",200,"OK",headers,input);
                } catch(Exception e) {return denied();}
            }
        });
        web.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if(fileCallback!=null) fileCallback.onReceiveValue(null);
                fileCallback=callback;
                Intent intent=new Intent(Intent.ACTION_OPEN_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("*/*");
                String[] accept=params.getAcceptTypes();
                if(accept!=null&&accept.length>0) {
                    boolean image=false;
                    for(String t:accept) if(t.contains("image")) image=true;
                    intent.putExtra(Intent.EXTRA_MIME_TYPES,image?new String[]{"image/jpeg","image/png","image/webp"}:new String[]{"application/json","text/plain","application/octet-stream"});
                }
                try {startActivityForResult(intent,PICK_FILE);} catch(Exception e) {callback.onReceiveValue(null);fileCallback=null;message("No file picker is available.");}
                return true;
            }
        });
        receiveSharedRecipe(getIntent());
        web.loadUrl("https://"+HOST+"/assets/index.html");
    }
    private void showWebViewHelp() {
        android.widget.TextView help=new android.widget.TextView(this);
        help.setText("Leggacy needs an updated Android System WebView\n\nUpdate Android System WebView or Chrome through your device’s app store, then reopen Leggacy. WebView version 80 or newer is required.\n\nYour saved recipes have not been changed. Do not uninstall Leggacy or clear its data.");
        help.setTextSize(20); help.setTextColor(Color.rgb(23,55,76));
        int padding=(int)(24*getResources().getDisplayMetrics().density); help.setPadding(padding,padding,padding,padding);
        android.widget.ScrollView scroll=new android.widget.ScrollView(this); scroll.setFillViewport(true); scroll.addView(help);
        root.removeAllViews();root.addView(scroll,new FrameLayout.LayoutParams(-1,-1));
    }
    private void configureEdgeToEdge() {
        // API 35+ enforces edge-to-edge. Older releases need an explicit opt-in.
        if (android.os.Build.VERSION.SDK_INT >= 30) {
            if (android.os.Build.VERSION.SDK_INT < 35) getWindow().setDecorFitsSystemWindows(false);
            WindowManager.LayoutParams attributes=getWindow().getAttributes();
            attributes.layoutInDisplayCutoutMode=WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS;
            getWindow().setAttributes(attributes);
        } else {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
        }
    }
    // Reconstructed from the verified 0.8.0 DEX; not represented as recovered original source.
    private boolean isSystemDarkMode() {
        return (getResources().getConfiguration().uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK) == android.content.res.Configuration.UI_MODE_NIGHT_YES;
    }
    private void applyAppearance(boolean dark) {
        if(destroyed || web==null || root==null)return;
        int color=dark?Color.rgb(23,35,48):Color.rgb(247,241,232);
        root.setBackgroundColor(color);web.setBackgroundColor(color);
        if(android.os.Build.VERSION.SDK_INT>=30 && getWindow().getInsetsController()!=null){
            int appearance=android.view.WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|android.view.WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS;
            getWindow().getInsetsController().setSystemBarsAppearance(dark?0:appearance,appearance);
        } else if(android.os.Build.VERSION.SDK_INT<30) {
            int flags=getWindow().getDecorView().getSystemUiVisibility();
            int light=View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR|View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
            getWindow().getDecorView().setSystemUiVisibility(dark?(flags & ~light):(flags|light));
        }
    }
    @Override public void onConfigurationChanged(android.content.res.Configuration configuration) {
        super.onConfigurationChanged(configuration);
        if(web!=null&&!destroyed)web.evaluateJavascript("window.dispatchEvent(new Event('savorshelf-system-theme'))",null);
    }
    @Override protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);setIntent(intent);receiveSharedRecipe(intent);
    }
    private void receiveSharedRecipe(Intent intent) {
        if(intent==null)return;
        String action=intent.getAction();
        if(!Intent.ACTION_SEND.equals(action)&&!Intent.ACTION_VIEW.equals(action))return;
        try {
            CharSequence sent=intent.getCharSequenceExtra(Intent.EXTRA_TEXT);
            if(sent!=null&&sent.length()<=2000000){sharedRecipe.set(sent.toString());notifySharedRecipe();return;}
            Uri uri=Intent.ACTION_SEND.equals(action)?(Uri)intent.getParcelableExtra(Intent.EXTRA_STREAM):intent.getData();
            if(uri==null||!"content".equals(uri.getScheme()))return;
            new Thread(()->{
                try(InputStream in=getContentResolver().openInputStream(uri)) {
                    if(in==null)throw new java.io.IOException();
                    java.io.ByteArrayOutputStream out=new java.io.ByteArrayOutputStream();byte[] buffer=new byte[4096];int n;
                    while((n=in.read(buffer))!=-1){if(out.size()+n>2000000)throw new java.io.IOException();out.write(buffer,0,n);}
                    sharedRecipe.set(new String(out.toByteArray(),StandardCharsets.UTF_8));notifySharedRecipe();
                }catch(Exception e){message("Could not read that recipe. Use a JSON or text file under 2 MB.");}
            },"OurTableSharedRecipe").start();
        }catch(Exception e){message("The shared recipe could not be opened. Paste its text instead.");}
    }
    private void notifySharedRecipe(){runOnUiThread(()->{if(!destroyed&&web!=null)web.evaluateJavascript("window.onIncomingRecipe && window.onIncomingRecipe()",null);});}
    private boolean isLocal(Uri uri) {return "https".equals(uri.getScheme())&&HOST.equals(uri.getHost());}
    private WebResourceResponse denied() {return new WebResourceResponse("text/plain","UTF-8",403,"Blocked",new HashMap<>(),new ByteArrayInputStream(new byte[0]));}
    private void message(String text) {runOnUiThread(()->Toast.makeText(this,text,Toast.LENGTH_LONG).show());}

    public class LocalBridge {
        @JavascriptInterface public boolean isSystemDark(){return isSystemDarkMode();}
        @JavascriptInterface public void setAppearance(String appearance){
            if("light".equals(appearance)||"dark".equals(appearance))runOnUiThread(()->applyAppearance("dark".equals(appearance)));
        }
        @JavascriptInterface public String consumeSharedRecipe(){return sharedRecipe.getAndSet("");}
        @JavascriptInterface public void requestChatGPT(String text){
            if(!ReleaseFeatures.CONNECTED_AI_ENABLED){message("Connected AI is not included in this beta.");return;}
            if(text==null||text.length()>200000){message("That request is too large to share.");return;}
            runOnUiThread(()->{
                ClipboardManager manager=(ClipboardManager)getSystemService(CLIPBOARD_SERVICE);
                manager.setPrimaryClip(ClipData.newPlainText("Leggacy recipe request",text));
                try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse("https://chatgpt.com/")));message("Request copied. Paste and send it in ChatGPT, then share or paste the recipe back into Leggacy.");}
                catch(Exception e){message("Request copied. Open ChatGPT and paste it there.");}
            });
        }

        /** Open the optional creator in the external browser; never load remote code in the privileged WebView. */
        @JavascriptInterface public String openCreatorPage(String url) {
            if(!ReleaseFeatures.CONNECTED_AI_ENABLED)return "Connected AI is not included in this beta.";
            try {
                if(url==null||url.length()>16000)return "The creator request is too long.";
                java.net.URI uri=new java.net.URI(url);String host=uri.getHost();
                if(!"https".equals(uri.getScheme())||host==null||!host.contains(".")||host.matches("[0-9.]+")||host.contains(":")||host.endsWith(".local")||host.endsWith(".localhost")||host.endsWith(".internal")||uri.getUserInfo()!=null||uri.getQuery()!=null||(uri.getPort()!=-1&&uri.getPort()!=443))return "Use a public HTTPS creator page.";
                runOnUiThread(()->{try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(url)));}catch(Exception e){message("No browser could open the creator page.");}});
                return "";
            }catch(Exception e){return "The creator page address is invalid.";}
        }

        @JavascriptInterface public synchronized String readData() {
            if(!store.getBaseFile().exists())return "";
            try{return new String(store.readFully(),StandardCharsets.UTF_8);}catch(Exception e){return "{unreadable-data";}
        }
        @JavascriptInterface public synchronized boolean writeData(String json) {
            if(json==null||json.length()>12000000)return false;
            FileOutputStream output=null;
            try {new org.json.JSONObject(json);output=store.startWrite();output.write(json.getBytes(StandardCharsets.UTF_8));store.finishWrite(output);return true;}
            catch(Exception e){if(output!=null)store.failWrite(output);return false;}
        }
        /** Configured URL is public; the app token is encrypted with Android Keystore. */
        @JavascriptInterface public synchronized String getAiConfig() {
            if(!ReleaseFeatures.CONNECTED_AI_ENABLED)return "{\"configured\":false,\"url\":\"\",\"available\":false}";
            try {org.json.JSONObject result=new org.json.JSONObject();String url=getPreferences(0).getString("aiUrl","");result.put("url",url);result.put("configured",!url.isEmpty()&&!readAiToken().isEmpty());return result.toString();}
            catch(Exception e){return "{\"configured\":false,\"url\":\"\"}";}
        }
        @JavascriptInterface public synchronized String setAiConfig(String url,String token) {
            if(!ReleaseFeatures.CONNECTED_AI_ENABLED)return "Connected AI is not included in this beta.";
            try {
                if(url==null||url.isEmpty()){getPreferences(0).edit().remove("aiUrl").remove("aiToken").remove("aiIv").apply();return "";}
                java.net.URI uri=new java.net.URI(url);String host=uri.getHost();
                if(!"https".equals(uri.getScheme())||host==null||!host.contains(".")||host.matches("[0-9.]+")||host.contains(":")||host.endsWith(".local")||host.endsWith(".localhost")||uri.getUserInfo()!=null||uri.getFragment()!=null||uri.getQuery()!=null||(uri.getPort()!=-1&&uri.getPort()!=443)||url.length()>1000)return "Use a public HTTPS endpoint without credentials, query parameters or a custom port.";
                if(token==null)token="";
                if(token.startsWith("sk-"))return "Do not enter a provider API key. Use the app token from your private server.";
                if(token.isEmpty()&&!url.equals(getPreferences(0).getString("aiUrl","")))return "Enter the app token when changing servers.";
                if(!token.isEmpty()){
                    if(token.length()<32||token.length()>500)return "Use an app token of 32–500 characters.";
                    javax.crypto.Cipher cipher=javax.crypto.Cipher.getInstance("AES/GCM/NoPadding");cipher.init(javax.crypto.Cipher.ENCRYPT_MODE,aiKey());
                    String encrypted=android.util.Base64.encodeToString(cipher.doFinal(token.getBytes(StandardCharsets.UTF_8)),android.util.Base64.NO_WRAP);
                    getPreferences(0).edit().putString("aiToken",encrypted).putString("aiIv",android.util.Base64.encodeToString(cipher.getIV(),android.util.Base64.NO_WRAP)).apply();
                }
                if(readAiToken().isEmpty())return "Enter an app access token.";
                getPreferences(0).edit().putString("aiUrl",url).apply();return "";
            } catch(Exception e){return "The connection could not be stored securely. Please try again.";}
        }
        @JavascriptInterface public void generateRecipe(String requestId,String payload) {
            if(!ReleaseFeatures.CONNECTED_AI_ENABLED){aiResult(requestId,"{\"error\":\"Connected AI is not included in this beta.\"}");return;}
            if(requestId==null||!requestId.matches("[a-zA-Z0-9-]{1,100}"))return;
            String url=getPreferences(0).getString("aiUrl",""), token=readAiToken();
            if(url.isEmpty()||token.isEmpty()){aiResult(requestId,"{\"error\":\"Configure the private AI connection first.\"}");return;}
            if(payload==null||payload.length()>6000){aiResult(requestId,"{\"error\":\"The request is too large.\"}");return;}
            if(!aiBusy.compareAndSet(false,true)){aiResult(requestId,"{\"error\":\"A recipe request is already in progress.\"}");return;}
            new Thread(()->{
                javax.net.ssl.HttpsURLConnection conn=null;
                try {
                    new org.json.JSONObject(payload);
                    conn=(javax.net.ssl.HttpsURLConnection)new java.net.URL(url).openConnection();
                    conn.setInstanceFollowRedirects(false);conn.setConnectTimeout(12000);conn.setReadTimeout(50000);conn.setRequestMethod("POST");conn.setDoOutput(true);conn.setRequestProperty("Content-Type","application/json");conn.setRequestProperty("Authorization","Bearer "+token);
                    try(OutputStream out=conn.getOutputStream()){out.write(payload.getBytes(StandardCharsets.UTF_8));}
                    int status=conn.getResponseCode();
                    if(status>=300&&status<400)throw new java.io.IOException("Redirect blocked");
                    InputStream input=status>=400?conn.getErrorStream():conn.getInputStream();if(input==null)throw new java.io.IOException("No response");
                    java.io.ByteArrayOutputStream bytes=new java.io.ByteArrayOutputStream();byte[] buffer=new byte[4096];int n;
                    try(InputStream in=input){while((n=in.read(buffer))!=-1){if(bytes.size()+n>200000)throw new java.io.IOException("Response too large");bytes.write(buffer,0,n);}}
                    String result=new String(bytes.toByteArray(),StandardCharsets.UTF_8);new org.json.JSONObject(result);aiResult(requestId,result);
                }catch(Exception e){aiResult(requestId,"{\"error\":\"Could not get a recipe from the configured HTTPS server. Check the connection, server status and app token. Your saved recipes are unchanged.\"}");}
                finally{if(conn!=null)conn.disconnect();aiBusy.set(false);}
            },"OurTableRecipeRequest").start();
        }
        @JavascriptInterface public void keepAwake(boolean keep) {runOnUiThread(()->{if(keep)getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);else getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);});}
        @JavascriptInterface public void copyText(String text) {runOnUiThread(()->{ClipboardManager manager=(ClipboardManager)getSystemService(CLIPBOARD_SERVICE);manager.setPrimaryClip(ClipData.newPlainText("Leggacy shopping list",text));});}
        @JavascriptInterface public void exportFile(String name,String content,String mime) {
            if(content==null||content.length()>12000000){message("That export is too large.");return;}
            runOnUiThread(()->{
                if(pendingExport!=null){message("Finish the current export first.");return;}
                pendingExport=content;
                Intent intent=new Intent(Intent.ACTION_CREATE_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("text/plain".equals(mime)?"text/plain":"application/json");
                intent.putExtra(Intent.EXTRA_TITLE,name.replaceAll("[^a-zA-Z0-9._-]","_"));
                try{startActivityForResult(intent,SAVE_FILE);}catch(Exception e){pendingExport=null;message("No save-file picker is available.");}
            });
        }
    }
    private javax.crypto.SecretKey aiKey() throws Exception {
        java.security.KeyStore store=java.security.KeyStore.getInstance("AndroidKeyStore");store.load(null);
        if(!store.containsAlias("ourtable-app-token")){
            javax.crypto.KeyGenerator gen=javax.crypto.KeyGenerator.getInstance(android.security.keystore.KeyProperties.KEY_ALGORITHM_AES,"AndroidKeyStore");
            gen.init(new android.security.keystore.KeyGenParameterSpec.Builder("ourtable-app-token",android.security.keystore.KeyProperties.PURPOSE_ENCRYPT|android.security.keystore.KeyProperties.PURPOSE_DECRYPT).setBlockModes(android.security.keystore.KeyProperties.BLOCK_MODE_GCM).setEncryptionPaddings(android.security.keystore.KeyProperties.ENCRYPTION_PADDING_NONE).build());gen.generateKey();
        }
        return (javax.crypto.SecretKey)store.getKey("ourtable-app-token",null);
    }
    private synchronized String readAiToken(){
        try{String encrypted=getPreferences(0).getString("aiToken","");if(encrypted.isEmpty())return "";
            byte[] iv=android.util.Base64.decode(getPreferences(0).getString("aiIv",""),android.util.Base64.NO_WRAP);
            javax.crypto.Cipher cipher=javax.crypto.Cipher.getInstance("AES/GCM/NoPadding");cipher.init(javax.crypto.Cipher.DECRYPT_MODE,aiKey(),new javax.crypto.spec.GCMParameterSpec(128,iv));
            return new String(cipher.doFinal(android.util.Base64.decode(encrypted,android.util.Base64.NO_WRAP)),StandardCharsets.UTF_8);
        }catch(Exception e){return "";}
    }
    private void aiResult(String requestId,String result){runOnUiThread(()->{if(!destroyed&&web!=null)web.evaluateJavascript("window.onAiResult && window.onAiResult("+org.json.JSONObject.quote(requestId)+","+org.json.JSONObject.quote(result)+")",null);});}
    @Override protected void onActivityResult(int request,int result,Intent data) {
        super.onActivityResult(request,result,data);
        if(request==PICK_FILE&&fileCallback!=null){fileCallback.onReceiveValue(result==RESULT_OK&&data!=null&&data.getData()!=null?new Uri[]{data.getData()}:null);fileCallback=null;}
        if(request==SAVE_FILE){String text=pendingExport;pendingExport=null;if(result==RESULT_OK&&data!=null&&data.getData()!=null&&text!=null){try(OutputStream out=getContentResolver().openOutputStream(data.getData(),"wt")){if(out==null)throw new java.io.IOException();out.write(text.getBytes(StandardCharsets.UTF_8));message("Backup saved.");}catch(Exception e){message("Backup could not be saved. Please try again.");}}}
    }
    private void handleBack() {if(web==null){finish();return;}web.evaluateJavascript("window.handleAndroidBack ? window.handleAndroidBack() : false",value->{if(!"true".equals(value)){if(web.canGoBack())web.goBack();else finish();}});}
    @SuppressWarnings("deprecation") @Override public void onBackPressed() {handleBack();}
    @Override protected void onDestroy() {destroyed=true;if(fileCallback!=null)fileCallback.onReceiveValue(null);if(web!=null){web.removeJavascriptInterface("AndroidBridge");web.destroy();}super.onDestroy();}
}
