package com.example.backendcod.persistence;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;

import com.example.backendcod.entities.IP;

public class IPDAO {
    private DBSource dbSource;
    private Connection conn;

    public IPDAO(DBSource dbS) throws SQLException {
        dbSource = dbS;
        conn = dbSource.getConnection();
    }

    private void getConnectionDB() {
        try {
            conn = dbSource.getConnection();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public IP getByIdNumber(String ip_number) {

        try {
            if (conn.isClosed()) {
                getConnectionDB();
            }
        } catch (SQLException e1) {
            e1.printStackTrace();
        }

        String query = "Select * from ip where ip_number=?";
        IP ip = null;

        try {
            PreparedStatement st = conn.prepareStatement(query);
            st.setString(1, ip_number);
            ResultSet rs = st.executeQuery();
            while (rs.next()) {
                Integer attempts = rs.getInt("attempts");
                Long time_of_block = rs.getLong("time_of_block");
                ip = new IP(ip_number, time_of_block, attempts);
            }
            st.close();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                conn.close();
            } catch (Exception e) {
            }
        }

        return ip;
    }

    public boolean insertIP(IP ip) {
        try {
            if (conn.isClosed()) {
                getConnectionDB();
            }
        } catch (SQLException e1) {
            e1.printStackTrace();
        }

        try {
            String queryUpdate = "INSERT INTO ip (ip_number,attempts,time_of_block) values(?, ?, ?)";
            PreparedStatement st = conn.prepareStatement(queryUpdate);
            st.setString(1, ip.getIP_number());
            st.setInt(2, ip.getAttempts());
            st.setLong(3, ip.getTimeinmillis());

            if (st.executeUpdate() == 1) {
                st.close();
                return true;
            } else {
                st.close();
                return false;
            }

        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                conn.close();
            } catch (Exception e) {
            }
        }

        return false;
    }

    public boolean updateAttempts(String ip_number) {
        try {
            if (conn.isClosed()) {
                getConnectionDB();
            }
        } catch (SQLException e1) {
            e1.printStackTrace();
        }

        Timestamp timestamp = new Timestamp(System.currentTimeMillis());

        String query = "UPDATE ip SET attempts = attempts+1,time_of_block =? WHERE ip_number=?";
        PreparedStatement stm = null;
        try {
            stm = conn.prepareStatement(query);
            stm.setLong(1, timestamp.getTime());
            stm.setString(2, ip_number);
            int res = stm.executeUpdate();
            if (res == 1) {
                System.out.println("UPDATE!!!");
                return true;
            } else {
                System.out.println("NOT UPDATE");
                return false;
            }

        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                conn.close();
            } catch (SQLException e) {
            }
        }
        return false;

    }

    public boolean resetAttempts(String ip_number, Integer attempts) {
        try {
            if (conn.isClosed()) {
                getConnectionDB();
            }
        } catch (SQLException e1) {
            e1.printStackTrace();
        }

        Timestamp timestamp = new Timestamp(System.currentTimeMillis());

        String query = "UPDATE ip SET attempts = ?,time_of_block =? WHERE ip_number=?";
        PreparedStatement stm = null;
        try {
            stm = conn.prepareStatement(query);
            stm.setInt(1, attempts);
            stm.setLong(2, timestamp.getTime());
            stm.setString(3, ip_number);
            int res = stm.executeUpdate();
            if (res == 1) {
                System.out.println("UPDATE!!!");
                return true;
            } else {
                System.out.println("NOT UPDATE");
                return false;
            }

        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                conn.close();
            } catch (SQLException e) {
            }
        }
        return false;

    }
}
