package com.bccard.gallery.backend.repository;


import org.springframework.data.jpa.repository.JpaRepository;

import com.bccard.gallery.backend.entity.Order;

import java.util.List;

public interface OrderRepository extends JpaRepository<Order, Integer> {

    List<Order> findByMemberIdOrderByIdDesc(int memberId);
}