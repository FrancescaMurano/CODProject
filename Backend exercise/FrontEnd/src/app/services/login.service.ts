import { Injectable } from '@angular/core';
import { HttpClient,HttpHeaders, HttpParams } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class LoginService {

  constructor(
    private httpClient: HttpClient
  ) {}

  login(json: any){
    return this.httpClient.post<string>("http://localhost:8080/home/login", json, {responseType: 'text' as 'json'});
  }
}
