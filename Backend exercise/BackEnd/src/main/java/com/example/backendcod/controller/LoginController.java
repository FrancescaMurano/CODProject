package com.example.backendcod.controller;
import com.example.backendcod.entities.LoginData;
import com.example.backendcod.persistence.DBManager;
import com.example.backendcod.utils.HttpUtils;

import jakarta.servlet.http.HttpServletRequest;

import java.net.http.HttpRequest;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;



@CrossOrigin(origins = "*", allowedHeaders = "*")
@RestController
@RequestMapping("/home")
public class LoginController {

    @PostMapping("/login")
    public ResponseEntity<Boolean> login(@RequestBody LoginData loginData, HttpServletRequest request) {
        DBManager.getDataSource();
        System.out.println(loginData.getUsername());
        System.out.println(loginData.getPassword());
        System.out.println(HttpUtils.getRequestIP(request));
        
        
        return ResponseEntity.ok(true);
    }

}
