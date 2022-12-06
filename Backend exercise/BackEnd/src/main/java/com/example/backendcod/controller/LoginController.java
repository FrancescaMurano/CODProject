package com.example.backendcod.controller;

import com.example.backendcod.entities.IP;
import com.example.backendcod.entities.LoginData;
import com.example.backendcod.persistence.DBManager;
import com.example.backendcod.persistence.DBSource;
import com.example.backendcod.persistence.IPDAO;
import com.example.backendcod.persistence.UserDAO;
import com.example.backendcod.utils.HttpUtils;

import jakarta.servlet.http.HttpServletRequest;

import java.net.http.HttpRequest;
import java.sql.Timestamp;
import java.sql.SQLException;

import org.json.JSONObject;
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
        String IP_number = HttpUtils.getRequestIP(request);
        IP ip = null;

        try {
            UserDAO userDAO = new UserDAO(DBManager.getDataSource());
            IPDAO ipdao = new IPDAO(DBManager.getDataSource());
            ip = ipdao.getByIdNumber(IP_number);

            if (userDAO.login(loginData)) {
                System.out.println("Esiste carlos");
                if (ip != null) { // è presente nella tabella
                    ipdao.resetAttempts(IP_number, 0);
                }
                return ResponseEntity.ok(true);
            } else {
                if (ip != null) { // è presente nella tabella
                    Long time = new Timestamp(System.currentTimeMillis()).getTime();
                    Long time_difference = time - ip.getTimeinmillis();
                    System.out.println("time_difference "+time_difference);
                    if (ip.getAttempts() > 3) {
                        // numero di tentativi > 3 ma non è passato 1 minuto
                        if (time_difference < 60000) {
                             
                            System.out.println("Login non corretto e sei bloccato");
                            ipdao.updateAttempts(IP_number);
                        } else {
                            // numero di tentativi > 3 ma è passato 1 minuto
                            ipdao.resetAttempts(IP_number, 1);
                            System.out.println("Login non corretto ma non sei più bloccato");
                        }
                    } else {
                        // numero di tentativi <=3 ma è passato 1 minuto
                        if (time_difference > 60000) {
                            System.out.println("Login non corretto, è passato un minuto");
                            ipdao.resetAttempts(IP_number, 1);
                        }
                        // numero di tentativi <=3 ma NON è passato 1 minuto
                        else {
                            System.out.println("Login non corretto, NON è passato un minuto");
                            ipdao.updateAttempts(IP_number);
                        }

                    }
                } else {
                    ipdao.insertIP(new IP(IP_number));
                }
                
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return ResponseEntity.ok(true);
    }

}
