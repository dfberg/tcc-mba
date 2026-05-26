package com.example.pocapi.integration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.example.pocapi.model.dto.AuthorDTO;
import com.example.pocapi.repository.AuthorRepository;
import com.example.pocapi.repository.BookRepository;
import com.example.pocapi.repository.ReviewRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.approvaltests.Approvals;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@DisplayName("Author API Integration Tests with Snapshots")
class AuthorApiIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Autowired
    private AuthorRepository authorRepository;
    
    @Autowired
    private BookRepository bookRepository;
    
    @Autowired
    private ReviewRepository reviewRepository;
    
    @BeforeEach
    void setUp() {
        // Clear data before each test
        reviewRepository.deleteAll();
        bookRepository.deleteAll();
        authorRepository.deleteAll();
    }
    
    @Test
    @DisplayName("should list all authors - snapshot test")
    void testGetAllAuthors_Snapshot() throws Exception {
        // Act
        MvcResult result = mockMvc.perform(get("/authors")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andReturn();
        
        String responseBody = result.getResponse().getContentAsString();
        
        // Assert - Snapshot verification
        Approvals.verify(responseBody);
    }
    
    @Test
    @DisplayName("should create author - snapshot test")
    void testCreateAuthor_Snapshot() throws Exception {
        // Arrange
        AuthorDTO authorDTO = AuthorDTO.builder()
                .name("Isaac Asimov")
                .email("isaac@example.com")
                .build();
        
        // Act
        MvcResult result = mockMvc.perform(post("/authors")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(authorDTO)))
                .andExpect(status().isCreated())
                .andReturn();
        
        String responseBody = result.getResponse().getContentAsString();
        
        // Assert - Snapshot verification
        Approvals.verify(responseBody);
    }
    
    @Test
    @DisplayName("should get author by id - snapshot test")
    void testGetAuthorById_Snapshot() throws Exception {
        // Arrange
        AuthorDTO authorDTO = AuthorDTO.builder()
                .name("J.R.R. Tolkien")
                .email("tolkien@example.com")
                .build();
        
        MvcResult createResult = mockMvc.perform(post("/authors")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(authorDTO)))
                .andExpect(status().isCreated())
                .andReturn();
        
        String createdJson = createResult.getResponse().getContentAsString();
        AuthorDTO createdAuthor = objectMapper.readValue(createdJson, AuthorDTO.class);
        
        // Act
        MvcResult result = mockMvc.perform(get("/authors/" + createdAuthor.getId())
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andReturn();
        
        String responseBody = result.getResponse().getContentAsString();
        
        // Assert - Snapshot verification
        Approvals.verify(responseBody);
    }
    
    @Test
    @DisplayName("should handle error when author not found - snapshot test")
    void testGetAuthorNotFound_Snapshot() throws Exception {
        // Act
        MvcResult result = mockMvc.perform(get("/authors/99999")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound())
                .andReturn();
        
        String responseBody = result.getResponse().getContentAsString();
        
        // Assert - Snapshot verification
        Approvals.verify(responseBody);
    }
}
