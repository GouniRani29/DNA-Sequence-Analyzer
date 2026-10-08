package project1.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import project1.entity.DnaAnalysis;

public interface DnaAnalysisRepository
        extends JpaRepository<DnaAnalysis, Long> {
}