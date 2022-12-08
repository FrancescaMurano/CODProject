package com.example.backendcod.controller;

import com.example.backendcod.entities.IP;
import com.example.backendcod.entities.LoginData;
import com.example.backendcod.persistence.DBManager;
import com.example.backendcod.persistence.IPDAO;
import com.example.backendcod.persistence.UserDAO;
import com.example.backendcod.utils.HttpUtils;

import jakarta.servlet.http.HttpServletRequest;

import java.sql.Timestamp;
import java.sql.SQLException;

import org.springframework.http.HttpStatus;
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
    public ResponseEntity<String> login(@RequestBody LoginData loginData, HttpServletRequest request) {
        DBManager.getDataSource();
        String IP_number = HttpUtils.getRequestIP(request);
        IP ip = null;

        try {
            UserDAO userDAO = new UserDAO(DBManager.getDataSource());
            IPDAO ipdao = new IPDAO(DBManager.getDataSource());
            ip = ipdao.getByIdNumber(IP_number);
            Long time = new Timestamp(System.currentTimeMillis()).getTime();
            if (userDAO.login(loginData)) {// è presente nella tabella
                if(ip!=null && (ip.getAttempts()<=3 || (time - ip.getTimeinmillis()) > 60000)){
                    ipdao.resetAttempts(IP_number, 0);
                    return new ResponseEntity<>("Sei loggato", HttpStatus.FOUND);
                }
                else if (ip == null){
                    return new ResponseEntity<>("Sei loggato", HttpStatus.FOUND);
                    // return ResponseEntity.ok("Sei loggato");
                }
                else{
                    ipdao.updateAttempts(IP_number);
                    return ResponseEntity.ok("Sei bloccato. Riprova tra 1 minuto");
                }
            } 
            else {
                if (ip != null) { // è presente nella tabella
                    if (ip.getAttempts() > 3) {
                        // numero di tentativi > 3 ma non è passato 1 minuto
                        if ((time - ip.getTimeinmillis()) < 60000) {
                            ipdao.updateAttempts(IP_number);
                            return ResponseEntity.ok("Sei bloccato. Riprova tra 1 minuto");
                        } else {
                            // numero di tentativi > 3 ma è passato 1 minuto
                            ipdao.resetAttempts(IP_number, 1);
                        }
                    } else {
                        // numero di tentativi <=3 ma è passato 1 minuto
                        if ((time - ip.getTimeinmillis()) > 60000) {
                            ipdao.resetAttempts(IP_number, 1);    
                        }
                        // numero di tentativi <=3 ma NON è passato 1 minuto
                        else {
                            ipdao.updateAttempts(IP_number);
                        }
                    }
                } 
                else 
                    ipdao.insertIP(new IP(IP_number));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return ResponseEntity.ok("Username o password non validi");
    } 
}
