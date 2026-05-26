package com.example.pocapi.service;

import com.example.pocapi.exception.ResourceNotFoundException;
import com.example.pocapi.exception.ValidationException;
import com.example.pocapi.model.dto.ReviewDTO;
import com.example.pocapi.model.entity.Book;
import com.example.pocapi.model.entity.Review;
import com.example.pocapi.repository.BookRepository;
import com.example.pocapi.repository.ReviewRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class ReviewService {
    
    private final ReviewRepository reviewRepository;
    private final BookRepository bookRepository;
    
    public List<ReviewDTO> getAllReviews() {
        return reviewRepository.findAll()
                .stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    public ReviewDTO getReviewById(Long id) {
        Review review = reviewRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Review", id));
        return convertToDTO(review);
    }
    
    public List<ReviewDTO> getReviewsByBookId(Long bookId) {
        // Verify book exists
        bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book", bookId));
        
        return reviewRepository.findByBookId(bookId)
                .stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    public ReviewDTO createReview(ReviewDTO reviewDTO) {
        validateReviewDTO(reviewDTO);
        
        Book book = bookRepository.findById(reviewDTO.getBookId())
                .orElseThrow(() -> new ResourceNotFoundException("Book", reviewDTO.getBookId()));
        
        Review review = new Review();
        review.setRating(reviewDTO.getRating());
        review.setContent(reviewDTO.getContent());
        review.setBook(book);
        review.validateRating();
        
        Review savedReview = reviewRepository.save(review);
        log.info("Review created with id: {}", savedReview.getId());
        
        return convertToDTO(savedReview);
    }
    
    public ReviewDTO updateReview(Long id, ReviewDTO reviewDTO) {
        validateReviewDTO(reviewDTO);
        
        Review review = reviewRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Review", id));
        
        Book book = bookRepository.findById(reviewDTO.getBookId())
                .orElseThrow(() -> new ResourceNotFoundException("Book", reviewDTO.getBookId()));
        
        review.setRating(reviewDTO.getRating());
        review.setContent(reviewDTO.getContent());
        review.setBook(book);
        review.validateRating();
        
        Review updatedReview = reviewRepository.save(review);
        log.info("Review updated with id: {}", updatedReview.getId());
        
        return convertToDTO(updatedReview);
    }
    
    public void deleteReview(Long id) {
        Review review = reviewRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Review", id));
        
        reviewRepository.delete(review);
        log.info("Review deleted with id: {}", id);
    }
    
    private void validateReviewDTO(ReviewDTO reviewDTO) {
        if (reviewDTO.getRating() == null || reviewDTO.getRating() < 1 || reviewDTO.getRating() > 5) {
            throw new ValidationException("Review rating must be between 1 and 5");
        }
        if (reviewDTO.getBookId() == null) {
            throw new ValidationException("Review must be associated with a book");
        }
    }
    
    private ReviewDTO convertToDTO(Review review) {
        return ReviewDTO.builder()
                .id(review.getId())
                .rating(review.getRating())
                .content(review.getContent())
                .bookId(review.getBook().getId())
                .bookTitle(review.getBook().getTitle())
                .build();
    }
}
