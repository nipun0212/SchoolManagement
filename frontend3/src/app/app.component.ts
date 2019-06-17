import { Component,OnInit } from '@angular/core';
import {Hero} from './hero'
import {HeroService} from './hero.service'
import {AuthGuard} from './auth-guard.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers:[HeroService]
})
export class AppComponent {
  constructor(private adminGuard:AuthGuard){
  }
subtitle = "";




}

