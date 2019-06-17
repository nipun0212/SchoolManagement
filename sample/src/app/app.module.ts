import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {MatSidenavModule} from '@angular/material';
import { AppComponent } from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatMenuModule} from '@angular/material';
import { RouterModule, Routes } from '@angular/router';
const routes : Routes = [
  
    { path: '', redirectTo: 'contact', pathMatch: 'full'},
    { path: 'crisis', loadChildren: 'app/crisis/crisis.module#CrisisModule' },
    { path: 'heroes', loadChildren: 'app/hero/hero.module.3#HeroModule' }
  
  ]
@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    MatSidenavModule,
    BrowserAnimationsModule,
    MatMenuModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
