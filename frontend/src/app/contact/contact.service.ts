import { Injectable } from '@angular/core';
import {Contact} from './contact'
const FETCH_LATENCY = 500;
const contacts: Contact[] = [
  new Contact(21, 'Sam Spade'),
  new Contact(22, 'Nick Danger'),
  new Contact(23, 'Nancy Drew')
];
@Injectable()
export class ContactService {

  // public contacts:Contact[];
  // constructor() { 
  // this.contacts.push(new Contact(21,'Nipun'));
  // this.contacts.push(new Contact(22,'Annu'));
  // this.contacts.push(new Contact(23,'Sarisha'));
  // }

  getContacts():Promise<Contact[]>{
    
      return new Promise<Contact[]>(resolve =>{
        setTimeout(()=>{resolve(contacts);},FETCH_LATENCY)
      })
  }

  getContact(id:number|string):Promise<Contact>{
    return this.getContacts().then(heroes=>heroes.find(hero=>hero.id ===+id))
  }


}

