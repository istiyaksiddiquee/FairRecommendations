import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({providedIn: 'root'})
export class LandingService {
    
    private URL = "http://localhost:8080/api/researchInterests";

    constructor(private http: HttpClient) {}

    getInformation() {
        try {
            return this.http.get(this.URL);
        } catch(err) {
            console.log(err);
        }
    }
}