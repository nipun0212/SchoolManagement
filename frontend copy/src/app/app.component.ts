import { Component,OnInit,AnimationTransitionEvent } from '@angular/core';
import {Hero} from './hero';
import {HeroService} from './hero.service';
import {AuthGuardService} from './guards/auth-guard.service';
import {AdminGuardService} from './guards/admin-guard.service';
import { Router,CanActivate,ActivatedRouteSnapshot,
  RouterStateSnapshot }    from '@angular/router';
// import {GoogleApiService} from "ng-gapi";
import 'rxjs/add/operator/toPromise';
import { Observable }        from 'rxjs/Observable';
// Observable class extensions
import 'rxjs/add/observable/of';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers:[HeroService]
})
export class AppComponent implements OnInit{
title:string;
myHero:string;
dashVisible:boolean = false;
heroes = ['Windstorm', 'Bombasto', 'Magneta', 'Tornado'];
constructor(){
  this.title = "Tour of Heroes";
  this.myHero = this.heroes[0];
  console.log("In app constructor");
  
}
ngOnInit(){
  console.log("In app onInit");
  
}


}

