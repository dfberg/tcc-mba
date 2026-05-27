package com.example.pocapi.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Profile;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;

@Configuration
@Profile("test")
public class TestTimeConfig {

    @Bean
    @Primary
    public Clock clock() {
        return Clock.fixed(Instant.parse("2026-05-26T13:25:34.690339900Z"), ZoneOffset.UTC);
    }
}
