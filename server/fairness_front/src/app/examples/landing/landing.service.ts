import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({providedIn: 'root'})
export class LandingService {
    
    private userURL = "http://localhost:8080/api/users";
    private recommendationURL = "http://localhost:8080/api/recommendation/?uuid=xyz1&research_interest=interest1&sim_weight=0.3&page_size=2&page_number=0";

    constructor(private http: HttpClient) {}

    getAllUsers() {
        try {
            return this.http.get(this.userURL);
        } catch(err) {
            console.log(err);
        }
    }

    getInformation() {
        try {
            return this.http.get(this.recommendationURL);
        } catch(err) {
            console.log(err);
        }
    }
}