import { Injectable }     from '@angular/core';
import { CanActivate }    from '@angular/router';
import '../gapi';
import { window } from '@angular/platform-browser/src/facade/browser';
import {User} from './user'
@Injectable()
export class AuthGuard implements CanActivate {
    u:User;
    constructor(){
        this.u = new User();
        this.getUser()
    }


  canActivate() {
return    window.gapi.client.schoolmanagement.getUser().then(a=>
    {   this.u.isAdmin = a.result.isAdmin;
        return a.result.isAdmin;})
}


isAdmin(){
   return this.u.isAdmin;
}

isActive(){
    console.log(this.u)
    return this.u.isActive;
 }
getUser(){
    window.gapi.client.schoolmanagement.getUser().then(a=>{
                this.u.isAdmin = a.result.isAdmin;
                this.u.isActive = a.result.isActive;
    });


}

}