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

        if(response === "You are logged"){
          sessionStorage.setItem("user", this.username);
          this.error = "";
          this.route.navigate(['home']);
        }
        else if(response === "You're blocked. Please try again in 1 minute"){
          this.error = "You're blocked. Please try again in 1 minute";
        }
        else{
          this.error = "Invalid username or password";
        }
      }
    );
  }
}
