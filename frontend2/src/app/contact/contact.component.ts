import { Component, OnInit } from '@angular/core';
import {Contact} from './contact';
import {ContactService} from './contact.service';
import {UserService} from '../core/user.service';
import {AuthGuard} from '../auth-guard.service';
import {FormControl, Validators} from '@angular/forms';
import { window } from '@angular/platform-browser/src/facade/browser';
import {Grade} from './data';

const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
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
  grades = [  "PreNursery",
  "Nursery" ,
   "JuniorKG" ,
   "SeniorKG" ,
   "First" ,
   "Second" ,
   "Third" ,
   "Fourth" ,
   "Fifth" ,
   "Sixth" ,
   "Seventh" ,
   "Eigth" ,
   "Nine" ,
   "Ten" ,
   "Eleven" ,
   "Twelth" ]
   grade=new Grade()
   name:string;
   orgSpecificName:string;
  constructor(private contactService:ContactService,private userService:UserService,
  private adminGuard:AuthGuard){
    
    this.userName = userService.userName;

   }

   onClick(){
     console.log(this.name);
     console.log(this.orgSpecificName);
     this.grade["name"] = this.name;
     this.grade["orgSpecificName"] = this.orgSpecificName;
     window.gapi.client.schoolmanagement.registerGrade(this.grade).then(e=>{
       console.log(e);
     })
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


  emailFormControl = new FormControl('', [
    Validators.required,
    Validators.pattern(EMAIL_REGEX)]);



}
