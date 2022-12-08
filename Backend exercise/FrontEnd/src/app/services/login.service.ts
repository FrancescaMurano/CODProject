import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
@Injectable({
  providedIn: 'root'
})
export class LoginService {

  constructor(
    private httpClient: HttpClient,
    private route: Router
  ) {}

  login(json: any){
    return this.httpClient.post<string>("http://localhost:8080/home/login", json, {responseType: 'text' as 'json'});
  }

  isLogged = () => (sessionStorage.getItem("user") != null) ? true : false;
}
