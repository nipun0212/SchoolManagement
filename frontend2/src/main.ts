import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';
import { environment } from './environments/environment';
import './gapi';
import { window } from '@angular/platform-browser/src/browser/facade/browser';
 console.log("dsjaldldj");
if (environment.production) {
      console.log("dsjaldldj");
    enableProdMode();
}
 console.log("dsjaldldj");
window.gapi.load('client',()=>
window.gapi.load('auth2',()=>
window.gapi.auth2.init({client_id:'557214639444-0rsmirikvhjt90hfonql1abcv38qevag.apps.googleusercontent.com'}).then(x=>
window.gapi.client.load('schoolmanagement', 'v1', null, '//' +"school-146605.appspot.com" + '/_ah/api').then(x=>{
// window.gapi.client.load('schoolmanagement', 'v1', null, '//' +"localhost:8080" + '/_ah/api').then(x=>{
    
console.log("dsjaldldj");
window.gapi.auth2.getAuthInstance().signIn().then(e=> platformBrowserDynamic().bootstrapModule(AppModule));

}))));

// platformBrowserDynamic().bootstrapModule(AppModule)