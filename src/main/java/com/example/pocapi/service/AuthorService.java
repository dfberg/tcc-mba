package com.example.pocapi.service;

import com.example.pocapi.exception.ResourceNotFoundException;
import com.example.pocapi.exception.ValidationException;
import com.example.pocapi.model.dto.AuthorDTO;
import com.example.pocapi.model.entity.Author;
import com.example.pocapi.repository.AuthorRepository;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthorService {
    
    private final AuthorRepository authorRepository;
    private final BookService bookService;
    private final ReviewService reviewService;
    
    @PostConstruct
    public void initData() {
        log.info("Initializing sample data...");
        
        // Create sample authors
        Author author1 = new Author();
        author1.setName("J.K. Rowling");
        author1.setEmail("jk@example.com");
        authorRepository.save(author1);
        
        Author author2 = new Author();
        author2.setName("George R.R. Martin");
        author2.setEmail("grrm@example.com");
        authorRepository.save(author2);
        
        log.info("Sample data initialized successfully");
    }
    
    public List<AuthorDTO> getAllAuthors() {
        return authorRepository.findAll()
                .stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    public AuthorDTO getAuthorById(Long id) {
        Author author = authorRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Author", id));
        return convertToDTO(author);
    }
    
    public AuthorDTO createAuthor(AuthorDTO authorDTO) {
        validateAuthorDTO(authorDTO);
        
        // Check if author with same email already exists
        if (authorRepository.findByEmail(authorDTO.getEmail()).isPresent()) {
            throw new ValidationException("Author with email " + authorDTO.getEmail() + " already exists");
        }
        
        Author author = new Author();
        author.setName(authorDTO.getName());
        author.setEmail(authorDTO.getEmail());
        
        Author savedAuthor = authorRepository.save(author);
        log.info("Author created with id: {}", savedAuthor.getId());
        
        return convertToDTO(savedAuthor);
    }
    
    public AuthorDTO updateAuthor(Long id, AuthorDTO authorDTO) {
        validateAuthorDTO(authorDTO);
        
        Author author = authorRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Author", id));
        
        // Check if new email is already in use by another author
        if (!author.getEmail().equals(authorDTO.getEmail()) && 
            authorRepository.findByEmail(authorDTO.getEmail()).isPresent()) {
            throw new ValidationException("Author with email " + authorDTO.getEmail() + " already exists");
        }
        
        author.setName(authorDTO.getName());
        author.setEmail(authorDTO.getEmail());
        
        Author updatedAuthor = authorRepository.save(author);
        log.info("Author updated with id: {}", updatedAuthor.getId());
        
        return convertToDTO(updatedAuthor);
    }
    
    public void deleteAuthor(Long id) {
        Author author = authorRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Author", id));
        
        authorRepository.delete(author);
        log.info("Author deleted with id: {}", id);
    }
    
    private void validateAuthorDTO(AuthorDTO authorDTO) {
        if (authorDTO.getName() == null || authorDTO.getName().isBlank()) {
            throw new ValidationException("Author name cannot be empty");
        }
        if (authorDTO.getEmail() == null || authorDTO.getEmail().isBlank()) {
            throw new ValidationException("Author email cannot be empty");
        }
        if (!authorDTO.getEmail().contains("@")) {
            throw new ValidationException("Author email must be valid");
        }
    }
    
    private AuthorDTO convertToDTO(Author author) {
        return AuthorDTO.builder()
                .id(author.getId())
                .name(author.getName())
                .email(author.getEmail())
                .build();
    }
}
