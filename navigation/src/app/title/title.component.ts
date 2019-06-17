import { Component, OnInit,Input } from '@angular/core';
import {UserService} from '../user.service'
@Component({
  selector: 'app-title',
  templateUrl: './title.component.html',
  styleUrls: ['./title.component.css']
})
export class TitleComponent implements OnInit {

  constructor(private userService:UserService) { 

    this.user = userService.userName;

  }

  ngOnInit() {
  }

  @Input() subtitle ='';
  title = "Tour of Heroes";
  user ='';
}
