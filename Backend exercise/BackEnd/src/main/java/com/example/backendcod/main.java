package com.example.backendcod;

import java.sql.Timestamp;
import java.sql.SQLException;

import org.json.*;
import org.springframework.security.crypto.bcrypt.BCrypt;

import com.example.backendcod.controller.LoginController;
import com.example.backendcod.entities.LoginData;
import com.example.backendcod.persistence.DBManager;
import com.example.backendcod.persistence.UserDAO;

public class main {
    public static void main(String[] args) throws InterruptedException{
        try {
            // JSONObject jsonObject = new JSONObject();

            // jsonObject.put("username", "carlo");
            // jsonObject.put("password", "montoya");
            LoginData login = new LoginData();
            UserDAO userDAO = new UserDAO(DBManager.getDataSource());
            login.setUsername("carlos");
            login.setPassword("ciao");
            LoginController controller = new LoginController();
            controller.login(login, null);
            // userDAO.login(login);
            // userDAO.login(login);
            // userDAO.login(login);
            // userDAO.login(login);
            // Thread.sleep(6001);
            // userDAO.login(login);
               // System.out.println("Esiste carlos");
            // else{
            //     System.out.println("Non esiste");
            // }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
