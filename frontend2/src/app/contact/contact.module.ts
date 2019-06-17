import { SharedModule }       from '../shared/shared.module';
import {ContactService} from './contact.service';
import { NgModule }           from '@angular/core';
import { ContactComponent }   from './contact.component';
import { ContactRoutingModule }   from './contact-routing.module';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatListModule,MatSidenavModule,MatToolbarModule,MatMenuModule} from '@angular/material';
import {MatFormFieldModule} from '@angular/material';
import {MatSelectModule} from '@angular/material';
import {MatInputModule} from '@angular/material';
import {MatGridListModule} from '@angular/material';


@NgModule({
    declarations: [
      ContactComponent,
   
    ],
    imports: [
      SharedModule,
        ContactRoutingModule,
        MatListModule,MatSidenavModule,MatToolbarModule,MatMenuModule,
        BrowserAnimationsModule,MatFormFieldModule,
        MatSelectModule,MatInputModule,MatGridListModule
    ],
    providers: [ContactService],
  })
  export class ContactModule { }