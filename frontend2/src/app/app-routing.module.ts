import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import {RouterModule,Routes} from '@angular/router';
import {AuthGuard} from './auth-guard.service';

const routes : Routes = [

  { path: '', redirectTo: 'contact', pathMatch: 'full'},
  { path: 'crisis', loadChildren: 'app/crisis/crisis.module#CrisisModule' ,canActivate: [AuthGuard]},
  { path: 'heroes', loadChildren: 'app/hero/hero.module.3#HeroModule',canActivate: [AuthGuard]}

]

@NgModule({
    imports :[RouterModule.forRoot(routes)],
    exports:[RouterModule]
})
export class AppRoutingModule {}