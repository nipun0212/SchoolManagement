import { Component, OnInit } from '@angular/core';
import {Contact} from './contact';
import {ContactService} from './contact.service';
import {UserService} from '../user.service';
@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent implements OnInit {

  userName:string;
  msg = 'Loading contacts ...';  
  contact:Contact;
  contacts:Contact[];

  constructor(private contactService:ContactService,private userService:UserService) {

    this.userName = userService.userName;

   }

  ngOnInit() {

    this.contactService.getContacts().then(contacts=>{
      this.contacts = contacts;
      this.msg = '';
      this.contact = contacts[0];
      console.log(this.contacts);
    })


  }

  next():void{
    let ix = 1 + this.contacts.indexOf(this.contact);
    if (ix >= this.contacts.length){ix = 0;}
    this.contact = this.contacts[ix];
  }

  onSubmit():void{
    this.displayMessage('Saved ' + this.contact.name);
  }

  newContact() {
    this.displayMessage('New contact');
    this.contact = {id: 42, name: ''};
    this.contacts.push(this.contact);
  }
  
  displayMessage(msg: string) {
    this.msg = msg;
    setTimeout(() => this.msg = '', 1500);
  }
}
