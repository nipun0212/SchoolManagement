import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { AuthGuard }            from '../auth-guard.service';

@NgModule({
  imports: [
    CommonModule
  ],

  providers: [
    AuthGuard
  ],
  declarations: [LoginComponent]
})
export class LoginModule { }
