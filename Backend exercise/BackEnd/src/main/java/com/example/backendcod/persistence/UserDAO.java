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

	public boolean login(JSONObject jsonCredentials) throws SQLException{
		try {if (conn.isClosed()){
			getConnectionDB();
		}
		} catch (SQLException e1) {
			e1.printStackTrace();
		}

		try{
			/*StringBuilder query = new StringBuilder("Select * from utente where username=? and password IN (");
			for(int i = 0; i < jsonCredentials.getJSONArray("password").length(); i++) {
				if (i > 0) {
					query.append(",");
				}
				query.append("?");
			}
			query.append(")");
			
			PreparedStatement st = conn.prepareStatement(query.toString());
			st.setString(1, jsonCredentials.getString("username"));
			
			int cont=2;
			for (int i = 0; i < jsonCredentials.getJSONArray("password").length(); i++) {
				st.setString(cont, jsonCredentials.getJSONArray("password").getString(i));
				cont++;
			}*/
			
			String query = "Select * from utente where username IN (?) and password IN ("+jsonCredentials.getJSONArray("password").toString()+")";
			PreparedStatement st = conn.prepareStatement(query);
			System.out.println(jsonCredentials.get("password").toString());
			System.out.println(jsonCredentials.getJSONArray("password").toString());
			st.setString(1, jsonCredentials.get("username").toString());
		//	st.setString(2, jsonCredentials.get("password").toString());
			ResultSet rs = st.executeQuery();
			if (rs.next()) {
				return true;
			}
			st.close();
		} 
		catch (SQLException e) {
			e.printStackTrace();
		}finally{try{conn.close();}catch(Exception e){}}
		return false;
	}
}