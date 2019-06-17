import { Component, OnInit } from '@angular/core';
import {AuthGuardService} from '../guards/auth-guard.service';
import {AdminGuardService} from '../guards/admin-guard.service';
@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})
export class TopBarComponent implements OnInit {

  constructor(private authGuardService:AuthGuardService,private adminGuardService:AdminGuardService) { }

  private dashboard:boolean = false;
  ngOnInit() {

     console.log(this.authGuardService.canActivate() && this.adminGuardService.canActivate());

  }
  

}
