import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { HeroDetailComponent } from './hero-detail/hero-detail.component';
import { HeroesComponent } from './heroes/heroes.component';
import {RouterModule,Routes} from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import {ClientConfig, GoogleApiModule, NG_GAPI_CONFIG} from "ng-gapi";
import {AuthGuardService} from './guards/auth-guard.service';
import {AdminGuardService} from './guards/admin-guard.service';


const routes : Routes = [

    {
        path:'heroes',
        component:HeroesComponent,
        canActivate: [AuthGuardService]
      },
      // {
      //   path:'',
      //   redirectTo:'/dashboard',
      //   pathMatch:'full',
      // },
      {
        path:'dashboard',
        component:DashboardComponent,
        canActivate: [AuthGuardService,AdminGuardService]
      },
      {
        path:'detail/:id',
        component:HeroDetailComponent,
        canActivate: [AuthGuardService]
       },
      {
        path:'**',
        redirectTo:'/dashboard'
      }

]
@NgModule({
     imports :[
      RouterModule.forRoot(routes
        // ,{ enableTracing: true }
      )],
    exports:[RouterModule]
})
export class AppRoutingModule {}