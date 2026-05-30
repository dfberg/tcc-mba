package com.example.pocapi.service;

import com.example.pocapi.exception.ResourceNotFoundException;
import com.example.pocapi.exception.ValidationException;
import com.example.pocapi.model.dto.BookDTO;
import com.example.pocapi.model.entity.Author;
import com.example.pocapi.model.entity.Book;
import com.example.pocapi.repository.AuthorRepository;
import com.example.pocapi.repository.BookRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class BookService {
    
    private final BookRepository bookRepository;
    private final AuthorRepository authorRepository;
    
    public List<BookDTO> getAllBooks() {
        return bookRepository.findAll()
                .stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    public BookDTO getBookById(Long id) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book", id));
        return convertToDTO(book);
    }
    
    public List<BookDTO> getBooksByAuthorId(Long authorId) {
        // Verify author exists
        authorRepository.findById(authorId)
                .orElseThrow(() -> new ResourceNotFoundException("Author", authorId));
        
        return bookRepository.findByAuthorId(authorId)
                .stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    public BookDTO createBook(BookDTO bookDTO) {
        validateBookDTO(bookDTO);
        
        Author author = authorRepository.findById(bookDTO.getAuthorId())
                .orElseThrow(() -> new ResourceNotFoundException("Author", bookDTO.getAuthorId()));
        
        // Check if book with same ISBN already exists
        if (bookRepository.findByIsbn(bookDTO.getIsbn()).isPresent()) {
            throw new ValidationException("Book with ISBN " + bookDTO.getIsbn() + " already exists");
        }
        
        Book book = new Book();
        book.setTitle(bookDTO.getTitle());
        book.setIsbn(bookDTO.getIsbn());
        book.setAuthor(author);
        
        Book savedBook = bookRepository.save(book);
        log.info("Book created with id: {}", savedBook.getId());
        
        return convertToDTO(savedBook);
    }
    
    public BookDTO updateBook(Long id, BookDTO bookDTO) {
        validateBookDTO(bookDTO);
        
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book", id));
        
        Author author = authorRepository.findById(bookDTO.getAuthorId())
                .orElseThrow(() -> new ResourceNotFoundException("Author", bookDTO.getAuthorId()));
        
        // Check if new ISBN is already in use by another book
        if (!book.getIsbn().equals(bookDTO.getIsbn()) && 
            bookRepository.findByIsbn(bookDTO.getIsbn()).isPresent()) {
            throw new ValidationException("Book with ISBN " + bookDTO.getIsbn() + " already exists");
        }
        
        book.setTitle(bookDTO.getTitle());
        book.setIsbn(bookDTO.getIsbn());
        book.setAuthor(author);
        
        Book updatedBook = bookRepository.save(book);
        log.info("Book updated with id: {}", updatedBook.getId());
        
        return convertToDTO(updatedBook);
    }
    
    public void deleteBook(Long id) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book", id));
        
        bookRepository.delete(book);
        log.info("Book deleted with id: {}", id);
    }
    
    private void validateBookDTO(BookDTO bookDTO) {
        if (bookDTO.getTitle() == null || bookDTO.getTitle().isBlank()) {
            throw new ValidationException("Book title cannot be empty");
        }
        if (bookDTO.getIsbn() == null || bookDTO.getIsbn().isBlank()) {
            throw new ValidationException("Book ISBN cannot be empty");
        }
        if (bookDTO.getAuthorId() == null) {
            throw new ValidationException("Book must have an author");
        }
    }
    
    private BookDTO convertToDTO(Book book) {
        return BookDTO.builder()
                .id(book.getId())
                .title(book.getTitle())
                .isbn(book.getIsbn())
                .authorId(book.getAuthor().getId())
                .authorName(book.getAuthor().getFirstName() + " " + book.getAuthor().getLastName())
                .build();
    }
}
