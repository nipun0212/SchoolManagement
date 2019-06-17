import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';
import { environment } from './environments/environment';
import {window} from '@angular/platform-browser/facade/browser'; 
import {Http} from '@angular/http';
import './gapi.js';
import 'hammerjs';
if (environment.production) {
  enableProdMode();
}
  
console.log("dsjaldldj");
window.gapi.load('client',()=>
window.gapi.load('auth2',()=>
window.gapi.client.load('schoolmanagement', 'v1', null, '//' +"school-146605.appspot.com" + '/_ah/api').then(x=>{
    console.log("dsjaldldj");
    platformBrowserDynamic().bootstrapModule(AppModule)
})));
