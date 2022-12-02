import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(
    private authService: AuthService
  ) { }

  username=""
  password=""

  ngOnInit(): void {}

  doLogin(){
    var json = {
      username: this.username,
      password: this.password
    }
    console.log(json.username)
    console.log(json.password)
    this.authService.authenticate(json).subscribe(
      response => {
        console.log(response)
      }
    );
      /*response => {
        if(response==true) {
          sessionStorage.setItem("user", this.email);
          sessionStorage.setItem("profile", this.tipo_login);
          this.autenticato = true;
          //this.route.navigate(['home', this.tipo_login]);
        }
        else {
            this.autenticato = false;
            this.messageService.add({key: 'saved', severity:'error', summary: 'Login', detail: 'Email o password errati'});
        }
      });*/
  }
}
