import { Component, OnInit } from '@angular/core';

import { LandingService } from './landing.service';


@Component({
    selector: 'app-landing',
    templateUrl: './landing.component.html',
    styleUrls: ['./landing.component.scss']
})

export class LandingComponent implements OnInit {
  simpleSlider = 40;
  page = 3;
  users = []
  with_bias = []
  bias_corrected = []

  constructor(private landingService: LandingService) { }

  ngOnInit() {
    this.loadUsers()
  }

  loadUsers() {
    this.landingService.getAllUsers().subscribe((data: any) => {
      this.users = data;
    });
  }

  loadData() {
    this.landingService.getInformation().subscribe((data: any) => {

      this.with_bias = data.with_bias;
      this.bias_corrected = data.bias_corrected;
    });
  }
  
  clickResponse1() {
    var infoDiv = document.getElementById('infoDiv1');
    infoDiv.hidden === true ? infoDiv.hidden = false : infoDiv.hidden = true;
  }

  clickResponse2() {
    var infoDiv = document.getElementById('infoDiv2');
    infoDiv.hidden === true ? infoDiv.hidden = false : infoDiv.hidden = true;
  }

  // getInformation() {
  //       try {
  //           return this.http.get(this.URL);
  //       } catch(err) {
  //           console.log(err);
  //       }
  //   }
}
