package com.example.backendcod.entities;

import java.sql.SQLException;

import com.example.backendcod.persistence.DBManager;
import com.example.backendcod.persistence.UserDAO;

public class User {
	private String username;
	private String password;
    private UserDAO userService;

    public User() throws SQLException {
        this.username = null;
        this.password = null;
        userService = new UserDAO(DBManager.getDataSource());
    }

    public User(String username, String password) throws SQLException{
        userService = new UserDAO(DBManager.getDataSource());
        this.username = username;
        this.password = password;
    }

    
    public void setUsername(String username) {
        this.username = username;
    }

    public void setPassword(String password) {
        this.password = password;
    }
   
    public String getUsername() {
        return username;
    }
    public String getPassword() {
        return password;
    }
    
    public String getJSONString() throws SQLException {
        String json = "{";
        json += "\"username\": \"" + username + "\",";
        json += "\"password\": \"" + password + "\",";
        json += "\"}";

        System.out.println("JSON "+ json);
        return json;
    }
}
