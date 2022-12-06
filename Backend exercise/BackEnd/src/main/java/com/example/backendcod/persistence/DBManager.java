package com.example.backendcod.persistence;

public class DBManager {

	private static DBManager instance = null;
	private static DBSource dataSource = null;
	
	static {
		try {
			Class.forName("org.postgresql.Driver");
			dataSource = new DBSource("jdbc:postgresql://localhost:5432/COD_DB","postgres","postgres");
            System.out.println("Success");
		} 
		catch (Exception e) {
			System.err.println("PostgresDAOFactory.class: failed to load postgresql JDBC driver\n"+e);
			e.printStackTrace();
		}
	}
	
	public static DBManager getInstance() {
		if (instance == null) {
			instance = new DBManager();
		}
		return instance;
	}
	
	private DBManager() {}
	
	public static DBSource getDataSource() {
		System.out.println("OK");
		return dataSource;
	}
	
}
