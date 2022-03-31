package com.thoughtworks.ssr.spring4shellpoc;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {
    @RequestMapping({"", "/"})
    public String test(User user) {
        return "ok";
    }
}
