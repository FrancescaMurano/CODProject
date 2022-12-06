package com.example.backendcod;

import java.sql.SQLException;

import org.json.*;

import com.example.backendcod.persistence.DBManager;
import com.example.backendcod.persistence.UserDAO;

public class main {
    public static void main(String[] args){
        try {
            JSONObject jsonObject = new JSONObject();
            JSONArray jsonArray = new JSONArray();
            jsonArray.put("montoya");
            jsonArray.put("ciciuzzu");
            jsonArray.put("cicciariajju");
            

            jsonObject.put("username", "carlos");
            jsonObject.put("password", jsonArray);
            UserDAO userDAO = new UserDAO(DBManager.getDataSource());
            if(userDAO.login(jsonObject)){
                System.out.println("Esiste carlos");
            }
            else{
                System.out.println("Non esiste");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
