import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, ɵassignExtraOptionsToRouter } from '@angular/router';
import { RouterStateSnapshot } from '@angular/router';
import { LoginService } from './login.service';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class RouteGuardHomeService {

  constructor(
    private route: Router
  ) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot)  {
    if (sessionStorage.getItem("user") != null)
    {
      this.route.navigate(['']);
      sessionStorage.removeItem("user");
    }
    return true;
  }
}
