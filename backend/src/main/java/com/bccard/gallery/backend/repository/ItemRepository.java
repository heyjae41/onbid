package com.bccard.gallery.backend.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.bccard.gallery.backend.entity.Item;

public interface ItemRepository extends JpaRepository<Item, Integer> {
	
	List<Item> findByIdIn(List<Integer> ids);

}
