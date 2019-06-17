import { Injectable } from '@angular/core';
import { CanActivate,ActivatedRouteSnapshot,
  RouterStateSnapshot }    from '@angular/router';
import {window} from '@angular/platform-browser/facade/browser'; 
import { Location }                 from '@angular/common';
import '../../gapi.js';
import { Router }            from '@angular/router';
import { Observable }        from 'rxjs/Observable';

// Observable class extensions
import 'rxjs/add/observable/of';
@Injectable()
export class AuthGuardService implements CanActivate {
  
  // canActivate(route1: ActivatedRouteSnapshot, state: RouterStateSnapshot):Observable<boolean>{
    
  //   const url = state.url;
    
  //   if (window.gapi.auth2.getAuthInstance() == null){
  //       this.signIn(url);
  //     }
    
  //   if (gapi.auth2.getAuthInstance().isSignedIn.get()){
  //     console.log("2nd if");
  //     return Observable.of(true);
  //   }
    
  //   return Observable.of(false);;

  // }

  // signIn(url:string):void{
      
  //   gapi.auth2.init({
  //     'client_id' : "557214639444-0rsmirikvhjt90hfonql1abcv38qevag.apps.googleusercontent.com",
  //     'scope':"openid profile email"
  //   })
  //   .then(gapi.auth2.getAuthInstance().signIn().then(()=>
  //   {
      
  //     if (gapi.auth2.getAuthInstance().isSignedIn.get()){
  //       this.route.navigate([url]);

  //     }
    
  //   }));
  
  // }
  // constructor(private route:Router,private location:Location) { }
  
  canActivate():boolean{
    

    
    if (window.gapi.auth2.getAuthInstance() == null){
        this.signIn();
      }
    
    if (gapi.auth2.getAuthInstance().isSignedIn.get()){
      console.log("2nd if");
      return true;
    }
    
    return false;

  }

  signIn():void{
      
    gapi.auth2.init({
      'client_id' : "557214639444-0rsmirikvhjt90hfonql1abcv38qevag.apps.googleusercontent.com",
      'scope':"openid profile email"
    })
    .then(gapi.auth2.getAuthInstance().signIn().then(()=>
    {
      
      if (gapi.auth2.getAuthInstance().isSignedIn.get()){

      }
    
    }));
  
  }
  constructor(private route:Router,private location:Location) { }


}
