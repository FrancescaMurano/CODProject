import { Component, OnInit } from '@angular/core';
import { LoginService } from '../services/login.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(
    private loginService: LoginService,
    private route: Router
  ) { }

  username=""
  password=""
  error=""
  ngOnInit(): void {}

  doLogin(){
    var json = {
      username: this.username,
      password: this.password
    }
    console.log(json.username)
    console.log(json.password)
    this.loginService.login(json).subscribe(
      response => {

        if(response === "Sei loggato"){
          sessionStorage.setItem("user", this.username);
          this.error = "";
          this.route.navigate(['home']);
        }
        else if(response === "Sei bloccato. Riprova tra 1 minuto"){
          this.error = "Sei bloccato. Riprova tra 1 minuto";
        }
        else{
          this.error = "Username o password non validi";
        }
      }
    );
  }
}
