import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { AppComponent } from './app.component';
import {MatButtonModule, MatCheckboxModule,MatSidenavModule,MatMenuModule,MatToolbarModule} from '@angular/material';
import {RouterModule} from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import {MdInputModule} from '@angular/material';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatCheckboxModule,
    MatSidenavModule,
    MatMenuModule,
    MatToolbarModule,
    RouterModule,
    RouterTestingModule,
    MdInputModule  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
