import { Injectable } from '@angular/core';
import {window} from '@angular/platform-browser/facade/browser'; 
import { Location }                 from '@angular/common';
import '../../gapi.js';
import { Router,CanActivate,ActivatedRouteSnapshot,
  RouterStateSnapshot }    from '@angular/router';
import {AuthGuardService} from './auth-guard.service'
@Injectable()
export class AdminGuardService {

  constructor() { }

  canActivate(){
    
    return window.gapi.client.schoolmanagement.getUser().then(a=> {
      console.log(a.result.isAdmin);
      return a.result.isAdmin;
    });

  }
    
}
