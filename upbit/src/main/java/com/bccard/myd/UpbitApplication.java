package com.bccard.myd;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class UpbitApplication {
	
	@GetMapping("/message")
	public String getMessage() {
		return "Hello Upbit";
	}

	public static void main(String[] args) {
		SpringApplication.run(UpbitApplication.class, args);
	}

}
