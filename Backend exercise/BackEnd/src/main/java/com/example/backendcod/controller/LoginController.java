package com.example.backendcod.controller;
import com.example.backendcod.entities.LoginData;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;



@CrossOrigin(origins = "*", allowedHeaders = "*")
@RestController
@RequestMapping("/restex")
public class LoginController {

    @PostMapping("/login")
    public ResponseEntity<Boolean> login(@RequestBody LoginData loginData) {
        System.out.println(loginData.getUsername());
        System.out.println(loginData.getPassword());
        return ResponseEntity.ok(true);
    }
}
