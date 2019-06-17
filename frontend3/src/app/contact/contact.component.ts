import { Component, Inject,OnInit } from '@angular/core';
import {Contact} from './contact';
import {ContactService} from './contact.service';
import {UserService} from '../core/user.service';
import {AuthGuard} from '../auth-guard.service';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

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
  tiles = [
    {text: 'One', cols: 3, rows: 1, color: 'lightblue'},
    {text: 'Two', cols: 1, rows: 2, color: 'lightgreen'},
    {text: 'Three', cols: 1, rows: 1, color: 'lightpink'},
    {text: 'Four', cols: 2, rows: 1, color: '#DDBDF1'},
  ];
  animal: string;
  name: string;
  constructor(private contactService:ContactService,private userService:UserService,
  private adminGuard:AuthGuard,public dialog: MatDialog) {

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

  openDialog(): void {
    let dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      width: '250px',
      data: { name: this.name, animal: this.animal }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.animal = result;
    });
  }

}

@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog-overview-example-dialog.html',
})
export class DialogOverviewExampleDialog {

  constructor(
    public dialogRef: MatDialogRef<DialogOverviewExampleDialog>,
    @Inject(MAT_DIALOG_DATA) public data: any) { }

  onNoClick(): void {
    this.dialogRef.close();
  }

}
