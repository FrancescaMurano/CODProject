package com.example.backendcod.persistence;

import java.sql.Array;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

import org.apache.tomcat.util.json.JSONParser;
import org.json.*;
import org.springframework.security.crypto.bcrypt.BCrypt;

import com.example.backendcod.entities.LoginData;

public class UserDAO {
    
    private DBSource dbSource;
	private Connection conn;
	
	
	public UserDAO(DBSource dbS) throws SQLException {
		dbSource = dbS;
        conn = dbSource.getConnection();
	}

	private void getConnectionDB(){
		try {
			conn = dbSource.getConnection();
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}

	public boolean login(LoginData credentials) throws SQLException{
		try {if (conn.isClosed()){
			getConnectionDB();
		}
		} catch (SQLException e1) {
			e1.printStackTrace();
		}

		
		String query = "SELECT password FROM utente WHERE username=?";
		PreparedStatement stm = null;
		try {
			stm = conn.prepareStatement(query);
			stm.setString(1, credentials.getUsername());

			ResultSet rs = stm.executeQuery();
			if(rs.next()){
				String hash_password = rs.getString("password");
	
				if(BCrypt.checkpw(credentials.getPassword(), hash_password)){
					return true;
				}

			}

		}catch (SQLException e) {
			e.printStackTrace();
		}finally{
			try {conn.close();} catch (SQLException e) {}
		}


		return false;
	}
}