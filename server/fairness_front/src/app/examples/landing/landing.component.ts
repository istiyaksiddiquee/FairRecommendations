import { Component, OnInit } from "@angular/core";

import { LandingService } from "./landing.service";

@Component({
  selector: "app-landing",
  templateUrl: "./landing.component.html",
  styleUrls: ["./landing.component.scss"],
})
export class LandingComponent implements OnInit {
  page = 1;
  page_size = 10;
  simpleSlider = 0.4;

  db_status = 1;

  keyword = "name";
  selected_user = null;
  collection_size = null;
  selected_interest = null;
  users = [];
  with_bias = [];
  bias_corrected = [];
  research_interests = [];

  female_ratio = null;

  constructor(private landingService: LandingService) {}

  ngOnInit() {
    this.InitialValidation();
  }

  InitialValidation() {
    this.landingService.performInitialCheckup().subscribe(
      (data: any) => {
        var input_div = document.getElementById("input_compartment");
        input_div.hidden = false;
        var slider_tooltip_list = document.getElementsByClassName('noUi-tooltip');
        slider_tooltip_list[0].style.bottom = "-320%"
        
        this.loadResearchInterests();
        this.loadUsers();
      },
      (error: any) => {
        var not_found_div = document.getElementById("not_found_div");
        not_found_div.hidden = false;
        console.log(error);
      }
    );
  }

  loadUsers() {
    const page_number = 0;
    const page_size = 902;

    this.landingService
      .getAllUsers(page_number, page_size)
      .subscribe((data: any) => {
        this.users = data;
      }, (error: any) => {
        console.log(error);
      });
  }

  loadResearchInterests() {
    this.landingService.getResearchInterestList().subscribe((data: any) => {
      for (let i = 0; i < data.research_interests.length; i++) {
        this.research_interests.push({ name: data.research_interests[i] });
      }
    });
  }

  loadRecommendationData() {
    const page_number = 0;

    const sim_weight = this.simpleSlider;
    const uuid = this.selected_user.uuid;
    const research_interest = this.selected_interest.name;

    this.landingService
      .getRecommendation(
        uuid,
        research_interest,
        sim_weight,
        page_number,
        this.page_size
      )
      .subscribe((data: any) => {
        this.with_bias = data.with_bias;
        this.bias_corrected = data.bias_corrected;
        this.collection_size = data.length;
        this.female_ratio = data.female_ratio;
        var pagination_div = document.getElementById("pagination_div");
        var result_section = document.getElementById("result_section");
        pagination_div.hidden = false;
        result_section.hidden = false;
      }, (error: any) => {
        console.log(error);
      });
  }

  clickResponse1(item) {
    var infoDiv = document.getElementById(item.uuid + "-biased");

    infoDiv.hidden === true
      ? (infoDiv.hidden = false)
      : (infoDiv.hidden = true);
  }

  clickResponse2(item) {
    var infoDiv = document.getElementById(item.uuid + "-corrected");

    infoDiv.hidden === true
      ? (infoDiv.hidden = false)
      : (infoDiv.hidden = true);
  }

  onPageChange(page_number) {
    // Page Number starts from 1, but, in the server, we need it to start from 0. So, we are subtracting 1 from it.
    var vanishingDiv = document.getElementById("vanishing_div"); 
    vanishingDiv.hidden = true; 

    page_number--;

    const sim_weight = this.simpleSlider;
    const uuid = this.selected_user.uuid;
    const research_interest = this.selected_interest.name;

    this.landingService
      .getRecommendation(
        uuid,
        research_interest,
        sim_weight,
        page_number,
        this.page_size
      )
      .subscribe((data: any) => {
        var vanishingDiv = document.getElementById("vanishing_div"); 
        vanishingDiv.hidden = false; 
        this.with_bias = data.with_bias;
        this.bias_corrected = data.bias_corrected;
        this.collection_size = data.length;
      });
  }

  userSelectEvent(item) {
    this.selected_user = item;
  }

  interestSelectEvent(item) {
    this.selected_interest = item;
  }

  userOnChangeSearch(search: string) {
    // fetch remote data from here
    // And reassign the 'data' which is binded to 'data' property.
  }

  interestOnChangeSearch(search: string) {
    // fetch remote data from here
    // And reassign the 'data' which is binded to 'data' property.
  }

  userOnFocused(e) {
    // do something
  }

  interestOnFocused(e) {
    // do something
  }

  // getInformation() {
  //       try {
  //           return this.http.get(this.URL);
  //       } catch(err) {
  //           console.log(err);
  //       }
  //   }

  biased_paper_card_click(item) {
    var infoDiv = document.getElementById(item.uuid + "-biased");

    infoDiv.hidden === true
      ? (infoDiv.hidden = false)
      : (infoDiv.hidden = true);
  }

  corrected_paper_card_click(item) {
    var infoDiv = document.getElementById(item.uuid + "-corrected");

    infoDiv.hidden === true
      ? (infoDiv.hidden = false)
      : (infoDiv.hidden = true);
  }

  indexChekcer(k, l) {
    console.log(k, l);
    if (k - (this.collection_size * (this.page - 1) + l) >= 0) {
      return true;
    } else if (this.collection_size * (this.page - 1) + l - k >= 0) {
      return true;
    }
    return false;
  }
}
