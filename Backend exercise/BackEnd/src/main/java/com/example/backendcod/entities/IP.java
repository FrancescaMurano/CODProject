package com.example.backendcod.entities;

import java.sql.Timestamp;

public class IP {
    private String IP_number;
    private Timestamp time;
    private Integer attempts;

    public IP(String IP_number, Timestamp time, Integer attempts){
        this.IP_number = IP_number;
        this.time = time;
        this.attempts = attempts;
    }

    public void setIP_number(String iP_number) {
        IP_number = iP_number;
    }

    public void setTime(Timestamp time) {
        this.time = time;
    }

    public void setAttempts(Integer attempts) {
        this.attempts = attempts;
    }

    public String getIP_number() {
        return IP_number;
    }

    public Timestamp getTime() {
        return time;
    }

    public Integer getAttempts() {
        return attempts;
    }

    public String toString(){
        return IP_number + ", " + time + ", " + attempts;
    }
}
