import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import {RouterModule} from '@angular/router';
import { CoreModule }       from './core/core.module';
import {AppRoutingModule} from './app-routing.module';
import {ContactModule} from './contact/contact.module'
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatListModule,MatSidenavModule,MatToolbarModule,MatMenuModule} from '@angular/material';
import {LoginModule} from './login/login.module'

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    ContactModule,
    AppRoutingModule,
    CoreModule.forRoot({userName: 'Nipun Madan'}),
    MatListModule,MatSidenavModule,MatToolbarModule,MatMenuModule,
    BrowserAnimationsModule,
    LoginModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
