import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RouteGuardHomeService } from './services/route-guard-home.service';
import { RouteGuardService } from './services/route-guard.service';

const routes: Routes = [
  {path:'home', component: HomeComponent, canActivate: [RouteGuardService]},
  {path:'', component: LoginComponent, canActivate: [RouteGuardHomeService]}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
