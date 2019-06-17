import { Injectable }     from '@angular/core';
import { CanActivate, RouterModule, Routes,Router  }    from '@angular/router';
import '../gapi';
import { window } from '@angular/platform-browser/src/facade/browser';
import {User} from './user'
@Injectable()
export class AuthGuard implements CanActivate {
    u:User;
    constructor(private router:Router  ){
        this.u = new User();
        this.getUser()
    }


canActivate() {
    console.log("nipun")

    if (this.u.isUser && this.u.isActive){
        return this.u.isActive;
    }
    else{
        this.router.navigate(['/contact'])
    }
}

isAdmin():boolean{
   return this.u.isAdmin;
}

isActive():boolean{
    return this.u.isActive;
 }

isStudent():boolean{
    return this.u.isStudent;
}

// isTeacher():Boolean{
//     return this.u.isTeacher;
// }

isOwner():boolean{
    return this.u.isAdmin;
}

isPrinciple():Boolean{
    return this.u.isPrincipal;
}

getUser(){
    window.gapi.client.schoolmanagement.getUser().then(a=>{
                this.u.isAdmin = a.result.isAdmin;
                this.u.isActive = a.result.isActive;
                this.u.isStudent = a.result.isStudent;
                this.u.isPrincipal = a.result.isPrincipal;
                this.u.isUser = a.result.isUser;
    },
()=>{
    console.log("Error Occured");
    // this.router.navigate(['/heroes'])
}
);


}

}